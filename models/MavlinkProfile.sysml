package MavlinkProfile {
    private import ScalarValues::*;

    enum def WireType {
        enum uint8_t;
        enum int8_t;
        enum uint16_t;
        enum int16_t;
        enum uint32_t;
        enum int32_t;
        enum uint64_t;
        enum int64_t;
        enum float;
        enum double;
        enum char;
    }

    metadata def MavlinkMessage {
        attribute id : Natural;
    }

    metadata def MavlinkField {
        attribute wireType : WireType;
        attribute units : String [0..1];
        attribute invalid : String [0..1];
        attribute autoVersion : Boolean [0..1];
    }

    metadata def MavlinkEnum {
        attribute bitmask : Boolean [0..1];
    }

    metadata def MavlinkEnumValue {
        attribute value : Natural;
    }
} // package MavlinkProfile
