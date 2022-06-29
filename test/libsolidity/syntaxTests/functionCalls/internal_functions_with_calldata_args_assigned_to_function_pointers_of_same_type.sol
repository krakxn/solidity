contract C {
    function g(bytes calldata b) pure external returns (bytes calldata) {
        return b[2:5];
    }

    function main() external returns (bytes memory) {
        function (bytes memory) external returns (bytes memory) ptr = this.g;
        bytes memory b = "123456789";
        return ptr(b);
    }
}
// ----
