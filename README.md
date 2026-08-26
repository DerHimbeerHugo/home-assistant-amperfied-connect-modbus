# Amperfied Connect Modbus

Custom integration for controlling an Amperfied Connect wallbox locally from
Home Assistant over Modbus TCP.

> **Status:** `0.1.0` is a test release. Test the behavior on the actual
> wallbox before relying on it unattended.

## Added wallbox behavior

| Home Assistant control | Wallbox behavior |
|---|---|
| **Eco mode on** | Enables the wallbox's automatic solar charging strategy (register 502). |
| **Eco mode off** | Returns to manual charging management and, by default, requests three-phase charging. |
| **Phase mode** | Selects one or three phases via register 501 and displays the actual state from register 5001. Manual selection is unavailable while Eco mode controls the phases. |
| **Stop charging** | Sets the charge-current command in register 261 to zero. It does not operate the wallbox's global Remote Lock. |
| **Vehicle disconnected** | If charging was stopped through register 261, restores the last target current once so that the next RFID-authorized session can start automatically. |

### Bounded phase verification

After each manual phase command, the integration waits for the switch duration
configured in register 503 plus five seconds. It then checks register 5001.

- If the requested state is present, nothing else is written.
- State `0` (switching) gets one additional 10-second grace check.
- A wrong final state causes exactly one retry of register 501.
- After that retry, the state is checked once more. A failure creates one
  persistent Home Assistant notification. There is no command loop.

If register 503 is unavailable, the documented 90-second default is used.

## Important distinction

**Remote Lock** is a global software lock for the wallbox. It is not the cable
latch and it is not used by the **Stop charging** button. Cable release remains
the responsibility of the vehicle after the charging current has been stopped.

## Options

The integration options contain three independent switches, enabled by default:

- switch to three phases when Eco mode is disabled;
- verify a phase command and retry once;
- restore charge enable after the vehicle is disconnected.

The Modbus polling interval remains configurable from 3 to 30 seconds.

## Compatibility

Phase and Eco entities are created only when their registers are present. The
phase-switch functions are intended for Connect Solar / Solar Pro hardware with
the internal phase-switch contactor. Other devices keep the supported basic
entities without being forced to expose unavailable controls.

The register implementation follows Amperfied's
[Connect series Modbus register documentation](https://www.amperfied.de/wp-content/uploads/2025/05/Documentation-Modbus-Register-Layout-connect-series-20250422.pdf).

## Manual installation for the first test

1. Copy `custom_components/amperfied_connect_modbus` into the same path below
   your Home Assistant configuration directory.
2. Restart Home Assistant completely.
3. Open **Settings → Devices & services → Add integration** and select
   **Amperfied Connect Modbus**.
4. Enter the wallbox IP address, port `502`, and its Modbus device ID.

The wallbox accepts only one Modbus TCP connection. Do not keep the old and new
config entries active at the same time. The old integration files may remain as
a backup, but unload or remove its config entry before configuring this one.

Because this integration has its own domain, Home Assistant creates a new config
entry and new unique IDs. After removing the old entry, existing entity IDs can
usually be assigned to the replacement entities again. Check any dashboards and
automations before deleting the old entity-registry entries.

## HACS installation and updates

After the repository has been published, add its URL in HACS as a custom
repository of category **Integration**. Releases are generated from the version
in `manifest.json`; HACS can then install later versions normally without
touching the original `heidelberg_energy_control` integration.

Repository URL:
[`DerHimbeerHugo/home-assistant-amperfied-connect-modbus`](https://github.com/DerHimbeerHugo/home-assistant-amperfied-connect-modbus)

## Safety

Phase switching operates mains-voltage contactors inside supported wallboxes.
Use it only with a compatible wallbox installation and follow the official
electrical installation and operating instructions.

## Origin and license

This project is derived from Schrolli91's MIT-licensed
[`heidelberg_energy_control`](https://github.com/Schrolli91/heidelberg_energy_control)
integration. The original copyright and MIT license are retained. This is an
independent community project and is not an official Amperfied integration.
