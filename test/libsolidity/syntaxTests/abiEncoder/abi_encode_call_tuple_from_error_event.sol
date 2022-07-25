contract C {
    event Ev();
    error Er();

    function f() public pure {
        abi.encodeCall(this.f, Ev());  // bad_cast
        abi.encodeCall(this.f, Er());  // bad_cast
    }
}
// ----
// TypeError 9062: (108-112): This type cannot be encoded.
// TypeError 9062: (159-163): This type cannot be encoded.
