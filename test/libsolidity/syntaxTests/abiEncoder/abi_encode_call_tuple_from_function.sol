contract C {
    function g0() internal {}
    function g1() internal returns (uint) {}
    function g2() internal returns (uint, uint) {}

    function f() public pure {
        abi.encodeCall(this.f, g0());
        abi.encodeCall(this.f, g1());
        abi.encodeCall(this.f, g2());
    }
}
// ----
// TypeError 9062: (202-206): This type cannot be encoded.
// TypeError 7515: (217-245): Expected a tuple with 0 components instead of a single non-tuple parameter.
// TypeError 9062: (278-282): This type cannot be encoded.
