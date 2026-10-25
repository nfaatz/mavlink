package MavlinkMini {
    private import MavlinkProfile::*;
    private import ISQ::*;
    private import CommonQuantities::*;
    private import MavlinkEnums::*;
    private import ScalarValues::*;

    item def HEARTBEAT {
        doc
        /* The heartbeat message shows that a system or component is present and responding. The type and autopilot fields (along with the message component id), allow the receiving system to treat further messages from this system appropriately (e.g. by laying out the user interface based on the autopilot). This microservice is documented at https://mavlink.io/en/services/heartbeat.html */
        @MavlinkMessage { id = 0; }

        attribute type : MAV_TYPE {
            doc
            /* Vehicle or component type. For a flight controller component the vehicle type (quadrotor, helicopter, etc.). For other components the component type (e.g. camera, gimbal, etc.). This should be used in preference to component id for identifying the component type. */
            @MavlinkField { wireType = WireType::uint8_t; }
        }
        attribute autopilot : MAV_AUTOPILOT {
            doc
            /* Autopilot type / class. Use MAV_AUTOPILOT_INVALID for components that are not flight controllers. */
            @MavlinkField { wireType = WireType::uint8_t; }
        }
        attribute base_mode : MAV_MODE_FLAG [0..*] {
            doc
            /* System mode bitmap. */
            @MavlinkField { wireType = WireType::uint8_t; }
        }
        attribute custom_mode : Natural {
            doc
            /* A bitfield for use for autopilot-specific flags */
            @MavlinkField { wireType = WireType::uint32_t; }
        }
        attribute system_status : MAV_STATE {
            doc
            /* System status flag. */
            @MavlinkField { wireType = WireType::uint8_t; }
        }
        attribute mavlink_version : Natural {
            doc
            /* MAVLink version, not writable by user, gets added by protocol because of magic data type: uint8_t_mavlink_version */
            @MavlinkField { wireType = WireType::uint8_t; autoVersion = true; }
        }
    }

    item def ATTITUDE {
        doc
        /* The attitude in the aeronautical frame
         * (right-handed, Z-down, Y-right, X-front, ZYX, intrinsic).
         */
        @MavlinkMessage { id = 30; }

        attribute time_boot_ms : DurationValue {
            doc
            /* Timestamp (time since system boot). */
            @MavlinkField { wireType = WireType::uint32_t; units = "ms"; }
        }
        attribute roll : AngularMeasureValue {
            doc
            /* Roll angle (-pi..+pi) */
            @MavlinkField { wireType = WireType::float; units = "rad"; }
        }
        attribute pitch : AngularMeasureValue {
            doc
            /* Pitch angle (-pi..+pi) */
            @MavlinkField { wireType = WireType::float; units = "rad"; }
        }
        attribute yaw : AngularMeasureValue {
            doc
            /* Yaw angle (-pi..+pi) */
            @MavlinkField { wireType = WireType::float; units = "rad"; }
        }
        attribute rollspeed : AngularVelocityValue {
            doc
            /* Roll angular speed */
            @MavlinkField { wireType = WireType::float; units = "rad/s"; }
        }
        attribute pitchspeed : AngularVelocityValue {
            doc
            /* Pitch angular speed */
            @MavlinkField { wireType = WireType::float; units = "rad/s"; }
        }
        attribute yawspeed : AngularVelocityValue {
            doc
            /* Yaw angular speed */
            @MavlinkField { wireType = WireType::float; units = "rad/s"; }
        }
    }
    item def GLOBAL_POSITION_INT {
        doc
        /* The filtered global position (e.g. fused GPS and accelerometers).
         * The position is in GPS-frame (right-handed, Z-up).
         * It is designed as scaled integer message since the resolution of float
         * is not sufficient.
         */
        @MavlinkMessage { id = 33; }

        attribute time_boot_ms : DurationValue {
            doc
            /* Timestamp (time since system boot). */
            @MavlinkField { wireType = WireType::uint32_t; units = "ms"; }
        }
        attribute lat : AngularMeasureValue {
            doc
            /* Latitude, expressed */
            @MavlinkField { wireType = WireType::int32_t; units = "degE7"; }
        }
        attribute lon : AngularMeasureValue {
            doc
            /* Longitude, expressed */
            @MavlinkField { wireType = WireType::int32_t; units = "degE7"; }
        }
        attribute alt : LengthValue {
            doc
            /* Altitude (MSL). Note that virtually all GPS modules provide both WGS84 and MSL. */
            @MavlinkField { wireType = WireType::int32_t; units = "mm"; }
        }
        attribute relative_alt : LengthValue {
            doc
            /* Altitude above home */
            @MavlinkField { wireType = WireType::int32_t; units = "mm"; }
        }
        attribute vx : VelocityComponentValue {
            doc
            /* Ground X Speed (Latitude, positive north) */
            @MavlinkField { wireType = WireType::int16_t; units = "cm/s"; }
        }
        attribute vy : VelocityComponentValue {
            doc
            /* Ground Y Speed (Longitude, positive east) */
            @MavlinkField { wireType = WireType::int16_t; units = "cm/s"; }
        }
        attribute vz : VelocityComponentValue {
            doc
            /* Ground Z Speed (Altitude, positive down) */
            @MavlinkField { wireType = WireType::int16_t; units = "cm/s"; }
        }
        attribute hdg : AngularMeasureValue {
            doc
            /* Vehicle heading (yaw angle), 0.0..359.99 degrees. If unknown, set to: UINT16_MAX */
            @MavlinkField { wireType = WireType::uint16_t; units = "cdeg"; invalid = "UINT16_MAX"; }
        }
    }
} // package MavlinkMini
