// GENERIERT aus test/mini.xml – nicht von Hand ändern
package MavlinkEnums {
    private import MavlinkProfile::*;

    enum def MAV_TYPE {
        doc
        /* MAVLINK component type reported in HEARTBEAT message. Flight controllers must report the type of the vehicle on which they are mounted (e.g. MAV_TYPE_OCTOROTOR). All other components must report a value appropriate for their type (e.g. a camera must use MAV_TYPE_CAMERA). */
        @MavlinkEnum;
        enum MAV_TYPE_GENERIC {
            doc
            /* Generic micro air vehicle */
            @MavlinkEnumValue { value = 0; }
        }
        enum MAV_TYPE_FIXED_WING {
            doc
            /* Fixed wing aircraft. */
            @MavlinkEnumValue { value = 1; }
        }
        enum MAV_TYPE_QUADROTOR {
            doc
            /* Quadrotor */
            @MavlinkEnumValue { value = 2; }
        }
        enum MAV_TYPE_COAXIAL {
            doc
            /* Coaxial helicopter */
            @MavlinkEnumValue { value = 3; }
        }
        enum MAV_TYPE_HELICOPTER {
            doc
            /* Normal helicopter with tail rotor. */
            @MavlinkEnumValue { value = 4; }
        }
        enum MAV_TYPE_ANTENNA_TRACKER {
            doc
            /* Ground installation */
            @MavlinkEnumValue { value = 5; }
        }
        enum MAV_TYPE_GCS {
            doc
            /* Operator control unit / ground control station */
            @MavlinkEnumValue { value = 6; }
        }
        enum MAV_TYPE_AIRSHIP {
            doc
            /* Airship, controlled */
            @MavlinkEnumValue { value = 7; }
        }
        enum MAV_TYPE_FREE_BALLOON {
            doc
            /* Free balloon, uncontrolled */
            @MavlinkEnumValue { value = 8; }
        }
        enum MAV_TYPE_ROCKET {
            doc
            /* Rocket */
            @MavlinkEnumValue { value = 9; }
        }
        enum MAV_TYPE_GROUND_ROVER {
            doc
            /* Ground rover */
            @MavlinkEnumValue { value = 10; }
        }
        enum MAV_TYPE_SURFACE_BOAT {
            doc
            /* Surface vessel, boat, ship */
            @MavlinkEnumValue { value = 11; }
        }
        enum MAV_TYPE_SUBMARINE {
            doc
            /* Submarine */
            @MavlinkEnumValue { value = 12; }
        }
        enum MAV_TYPE_HEXAROTOR {
            doc
            /* Hexarotor */
            @MavlinkEnumValue { value = 13; }
        }
        enum MAV_TYPE_OCTOROTOR {
            doc
            /* Octorotor */
            @MavlinkEnumValue { value = 14; }
        }
        enum MAV_TYPE_TRICOPTER {
            doc
            /* Tricopter */
            @MavlinkEnumValue { value = 15; }
        }
        enum MAV_TYPE_FLAPPING_WING {
            doc
            /* Flapping wing */
            @MavlinkEnumValue { value = 16; }
        }
        enum MAV_TYPE_KITE {
            doc
            /* Kite */
            @MavlinkEnumValue { value = 17; }
        }
        enum MAV_TYPE_ONBOARD_CONTROLLER {
            doc
            /* Onboard companion controller */
            @MavlinkEnumValue { value = 18; }
        }
        enum MAV_TYPE_VTOL_TAILSITTER_DUOROTOR {
            doc
            /* Two-rotor Tailsitter VTOL that additionally uses control surfaces in vertical operation. Note, value previously named MAV_TYPE_VTOL_DUOROTOR. */
            @MavlinkEnumValue { value = 19; }
        }
        enum MAV_TYPE_VTOL_TAILSITTER_QUADROTOR {
            doc
            /* Quad-rotor Tailsitter VTOL using a V-shaped quad config in vertical operation. Note: value previously named MAV_TYPE_VTOL_QUADROTOR. */
            @MavlinkEnumValue { value = 20; }
        }
        enum MAV_TYPE_VTOL_TILTROTOR {
            doc
            /* Tiltrotor VTOL. Fuselage and wings stay (nominally) horizontal in all flight phases. It able to tilt (some) rotors to provide thrust in cruise flight. */
            @MavlinkEnumValue { value = 21; }
        }
        enum MAV_TYPE_VTOL_FIXEDROTOR {
            doc
            /* VTOL with separate fixed rotors for hover and cruise flight. Fuselage and wings stay (nominally) horizontal in all flight phases. */
            @MavlinkEnumValue { value = 22; }
        }
        enum MAV_TYPE_VTOL_TAILSITTER {
            doc
            /* Tailsitter VTOL. Fuselage and wings orientation changes depending on flight phase: vertical for hover, horizontal for cruise. Use more specific VTOL MAV_TYPE_VTOL_TAILSITTER_DUOROTOR or MAV_TYPE_VTOL_TAILSITTER_QUADROTOR if appropriate. */
            @MavlinkEnumValue { value = 23; }
        }
        enum MAV_TYPE_VTOL_TILTWING {
            doc
            /* Tiltwing VTOL. Fuselage stays horizontal in all flight phases. The whole wing, along with any attached engine, can tilt between vertical and horizontal mode. */
            @MavlinkEnumValue { value = 24; }
        }
        enum MAV_TYPE_VTOL_RESERVED5 {
            doc
            /* VTOL reserved 5 */
            @MavlinkEnumValue { value = 25; }
        }
        enum MAV_TYPE_GIMBAL {
            doc
            /* Gimbal */
            @MavlinkEnumValue { value = 26; }
        }
        enum MAV_TYPE_ADSB {
            doc
            /* ADSB system */
            @MavlinkEnumValue { value = 27; }
        }
        enum MAV_TYPE_PARAFOIL {
            doc
            /* Steerable, nonrigid airfoil */
            @MavlinkEnumValue { value = 28; }
        }
        enum MAV_TYPE_DODECAROTOR {
            doc
            /* Dodecarotor */
            @MavlinkEnumValue { value = 29; }
        }
        enum MAV_TYPE_CAMERA {
            doc
            /* Camera */
            @MavlinkEnumValue { value = 30; }
        }
        enum MAV_TYPE_CHARGING_STATION {
            doc
            /* Charging station */
            @MavlinkEnumValue { value = 31; }
        }
        enum MAV_TYPE_FLARM {
            doc
            /* FLARM collision avoidance system */
            @MavlinkEnumValue { value = 32; }
        }
        enum MAV_TYPE_SERVO {
            doc
            /* Servo */
            @MavlinkEnumValue { value = 33; }
        }
        enum MAV_TYPE_ODID {
            doc
            /* Open Drone ID. See https://mavlink.io/en/services/opendroneid.html. */
            @MavlinkEnumValue { value = 34; }
        }
        enum MAV_TYPE_DECAROTOR {
            doc
            /* Decarotor */
            @MavlinkEnumValue { value = 35; }
        }
        enum MAV_TYPE_BATTERY {
            doc
            /* Battery */
            @MavlinkEnumValue { value = 36; }
        }
        enum MAV_TYPE_PARACHUTE {
            doc
            /* Parachute */
            @MavlinkEnumValue { value = 37; }
        }
        enum MAV_TYPE_LOG {
            doc
            /* Log */
            @MavlinkEnumValue { value = 38; }
        }
        enum MAV_TYPE_OSD {
            doc
            /* OSD */
            @MavlinkEnumValue { value = 39; }
        }
        enum MAV_TYPE_IMU {
            doc
            /* IMU */
            @MavlinkEnumValue { value = 40; }
        }
        enum MAV_TYPE_GPS {
            doc
            /* GPS */
            @MavlinkEnumValue { value = 41; }
        }
        enum MAV_TYPE_WINCH {
            doc
            /* Winch */
            @MavlinkEnumValue { value = 42; }
        }
        enum MAV_TYPE_GENERIC_MULTIROTOR {
            doc
            /* Generic multirotor that does not fit into a specific type or whose type is unknown */
            @MavlinkEnumValue { value = 43; }
        }
        enum MAV_TYPE_ILLUMINATOR {
            doc
            /* Illuminator. An illuminator is a light source that is used for lighting up dark areas external to the system: e.g. a torch or searchlight (as opposed to a light source for illuminating the system itself, e.g. an indicator light). */
            @MavlinkEnumValue { value = 44; }
        }
        enum MAV_TYPE_SPACECRAFT_ORBITER {
            doc
            /* Orbiter spacecraft. Includes satellites orbiting terrestrial and extra-terrestrial bodies. Follows NASA Spacecraft Classification. */
            @MavlinkEnumValue { value = 45; }
        }
        enum MAV_TYPE_GROUND_QUADRUPED {
            doc
            /* A generic four-legged ground vehicle (e.g., a robot dog). */
            @MavlinkEnumValue { value = 46; }
        }
        enum MAV_TYPE_VTOL_GYRODYNE {
            doc
            /* VTOL hybrid of helicopter and autogyro. It has a main rotor for lift and separate propellers for forward flight. The rotor must be powered for hover but can autorotate in cruise flight. See: https://en.wikipedia.org/wiki/Gyrodyne */
            @MavlinkEnumValue { value = 47; }
        }
        enum MAV_TYPE_GRIPPER {
            doc
            /* Gripper */
            @MavlinkEnumValue { value = 48; }
        }
        enum MAV_TYPE_RADIO {
            doc
            /* Radio */
            @MavlinkEnumValue { value = 49; }
        }
    }

    enum def MAV_AUTOPILOT {
        doc
        /* Micro air vehicle / autopilot classes. This identifies the individual model. */
        @MavlinkEnum;
        enum MAV_AUTOPILOT_GENERIC {
            doc
            /* Generic autopilot, full support for everything */
            @MavlinkEnumValue { value = 0; }
        }
        enum MAV_AUTOPILOT_RESERVED {
            doc
            /* Reserved for future use. */
            @MavlinkEnumValue { value = 1; }
        }
        enum MAV_AUTOPILOT_SLUGS {
            doc
            /* SLUGS autopilot, http://slugsuav.soe.ucsc.edu */
            @MavlinkEnumValue { value = 2; }
        }
        enum MAV_AUTOPILOT_ARDUPILOTMEGA {
            doc
            /* ArduPilot - Plane/Copter/Rover/Sub/Tracker, https://ardupilot.org */
            @MavlinkEnumValue { value = 3; }
        }
        enum MAV_AUTOPILOT_OPENPILOT {
            doc
            /* OpenPilot, http://openpilot.org */
            @MavlinkEnumValue { value = 4; }
        }
        enum MAV_AUTOPILOT_GENERIC_WAYPOINTS_ONLY {
            doc
            /* Generic autopilot only supporting simple waypoints */
            @MavlinkEnumValue { value = 5; }
        }
        enum MAV_AUTOPILOT_GENERIC_WAYPOINTS_AND_SIMPLE_NAVIGATION_ONLY {
            doc
            /* Generic autopilot supporting waypoints and other simple navigation commands */
            @MavlinkEnumValue { value = 6; }
        }
        enum MAV_AUTOPILOT_GENERIC_MISSION_FULL {
            doc
            /* Generic autopilot supporting the full mission command set */
            @MavlinkEnumValue { value = 7; }
        }
        enum MAV_AUTOPILOT_INVALID {
            doc
            /* No valid autopilot, e.g. a GCS or other MAVLink component */
            @MavlinkEnumValue { value = 8; }
        }
        enum MAV_AUTOPILOT_PPZ {
            doc
            /* PPZ UAV - http://nongnu.org/paparazzi */
            @MavlinkEnumValue { value = 9; }
        }
        enum MAV_AUTOPILOT_UDB {
            doc
            /* UAV Dev Board */
            @MavlinkEnumValue { value = 10; }
        }
        enum MAV_AUTOPILOT_FP {
            doc
            /* FlexiPilot */
            @MavlinkEnumValue { value = 11; }
        }
        enum MAV_AUTOPILOT_PX4 {
            doc
            /* PX4 Autopilot - http://px4.io/ */
            @MavlinkEnumValue { value = 12; }
        }
        enum MAV_AUTOPILOT_SMACCMPILOT {
            doc
            /* SMACCMPilot - http://smaccmpilot.org */
            @MavlinkEnumValue { value = 13; }
        }
        enum MAV_AUTOPILOT_AUTOQUAD {
            doc
            /* AutoQuad -- http://autoquad.org */
            @MavlinkEnumValue { value = 14; }
        }
        enum MAV_AUTOPILOT_ARMAZILA {
            doc
            /* Armazila -- http://armazila.com */
            @MavlinkEnumValue { value = 15; }
        }
        enum MAV_AUTOPILOT_AEROB {
            doc
            /* Aerob -- http://aerob.ru */
            @MavlinkEnumValue { value = 16; }
        }
        enum MAV_AUTOPILOT_ASLUAV {
            doc
            /* ASLUAV autopilot -- http://www.asl.ethz.ch */
            @MavlinkEnumValue { value = 17; }
        }
        enum MAV_AUTOPILOT_SMARTAP {
            doc
            /* SmartAP Autopilot - http://sky-drones.com */
            @MavlinkEnumValue { value = 18; }
        }
        enum MAV_AUTOPILOT_AIRRAILS {
            doc
            /* AirRails - http://uaventure.com */
            @MavlinkEnumValue { value = 19; }
        }
        enum MAV_AUTOPILOT_REFLEX {
            doc
            /* Fusion Reflex - https://fusion.engineering */
            @MavlinkEnumValue { value = 20; }
        }
        enum MAV_AUTOPILOT_FLIX {
            doc
            /* Flix quadcopter - https://quadcopter.dev */
            @MavlinkEnumValue { value = 21; }
        }
    }

    enum def MAV_MODE_FLAG {
        doc
        /* These flags encode the MAV mode, see MAV_MODE enum for useful combinations. */
        @MavlinkEnum { bitmask = true; }
        enum MAV_MODE_FLAG_SAFETY_ARMED {
            doc
            /* 0b10000000 MAV safety set to armed. Motors are enabled / running / can start. Ready to fly. Additional note: this flag is to be ignored when sent in the command MAV_CMD_DO_SET_MODE and MAV_CMD_COMPONENT_ARM_DISARM shall be used instead. The flag can still be used to report the armed state. */
            @MavlinkEnumValue { value = 128; }
        }
        enum MAV_MODE_FLAG_MANUAL_INPUT_ENABLED {
            doc
            /* 0b01000000 remote control input is enabled. */
            @MavlinkEnumValue { value = 64; }
        }
        enum MAV_MODE_FLAG_HIL_ENABLED {
            doc
            /* 0b00100000 hardware in the loop simulation. All motors / actuators are blocked, but internal software is full operational. */
            @MavlinkEnumValue { value = 32; }
        }
        enum MAV_MODE_FLAG_STABILIZE_ENABLED {
            doc
            /* 0b00010000 system stabilizes electronically its attitude (and optionally position). It needs however further control inputs to move around. */
            @MavlinkEnumValue { value = 16; }
        }
        enum MAV_MODE_FLAG_GUIDED_ENABLED {
            doc
            /* 0b00001000 guided mode enabled, system flies waypoints / mission items. */
            @MavlinkEnumValue { value = 8; }
        }
        enum MAV_MODE_FLAG_AUTO_ENABLED {
            doc
            /* 0b00000100 autonomous mode enabled, system finds its own goal positions. Guided flag can be set or not, depends on the actual implementation. */
            @MavlinkEnumValue { value = 4; }
        }
        enum MAV_MODE_FLAG_TEST_ENABLED {
            doc
            /* 0b00000010 system has a test mode enabled. This flag is intended for temporary system tests and should not be used for stable implementations. */
            @MavlinkEnumValue { value = 2; }
        }
        enum MAV_MODE_FLAG_CUSTOM_MODE_ENABLED {
            doc
            /* 0b00000001 system-specific custom mode is enabled. When using this flag to enable a custom mode all other flags should be ignored. */
            @MavlinkEnumValue { value = 1; }
        }
    }

    enum def MAV_STATE {
        @MavlinkEnum;
        enum MAV_STATE_UNINIT {
            doc
            /* Uninitialized system, state is unknown. */
            @MavlinkEnumValue { value = 0; }
        }
        enum MAV_STATE_BOOT {
            doc
            /* System is booting up. */
            @MavlinkEnumValue { value = 1; }
        }
        enum MAV_STATE_CALIBRATING {
            doc
            /* System is calibrating and not flight-ready. */
            @MavlinkEnumValue { value = 2; }
        }
        enum MAV_STATE_STANDBY {
            doc
            /* System is grounded and on standby. It can be launched any time. */
            @MavlinkEnumValue { value = 3; }
        }
        enum MAV_STATE_ACTIVE {
            doc
            /* System is active and might be already airborne. Motors are engaged. */
            @MavlinkEnumValue { value = 4; }
        }
        enum MAV_STATE_CRITICAL {
            doc
            /* System is in a non-normal flight mode (failsafe). It can however still navigate. */
            @MavlinkEnumValue { value = 5; }
        }
        enum MAV_STATE_EMERGENCY {
            doc
            /* System is in a non-normal flight mode (failsafe). It lost control over parts or over the whole airframe. It is in mayday and going down. */
            @MavlinkEnumValue { value = 6; }
        }
        enum MAV_STATE_POWEROFF {
            doc
            /* System just initialized its power-down sequence, will shut down now. */
            @MavlinkEnumValue { value = 7; }
        }
        enum MAV_STATE_FLIGHT_TERMINATION {
            doc
            /* System is terminating itself (failsafe or commanded). */
            @MavlinkEnumValue { value = 8; }
        }
    }
} // package MavlinkEnums
