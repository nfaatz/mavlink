package MavlinkMini {
    private import MavlinkProfile::*;
    private import ISQ::*;
    private import CommonQuantities::*;
    private import MavlinkEnums::*;
    private import ScalarValues::*;

    item def HEARTBEAT {
        doc
        /* The heartbeat message shows that a system or component
         * is present and responding.
         */
        @MavlinkMessage { id = 0; }

        attribute type : MAV_TYPE {
            @MavlinkField { wireType = WireType::uint8_t; }
        }
        attribute autopilot : MAV_AUTOPILOT {
            @MavlinkField { wireType = WireType::uint8_t; }
        }
        attribute base_mode : MAV_MODE_FLAG [0..*] {
            @MavlinkField { wireType = WireType::uint8_t; }
        }
        attribute custom_mode : Natural {
            @MavlinkField { wireType = WireType::uint32_t; }
        }
        attribute system_status : MAV_STATE {
            @MavlinkField { wireType = WireType::uint8_t; }
        }
        attribute mavlink_version : Natural {
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
