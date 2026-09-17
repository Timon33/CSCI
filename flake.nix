{
  description = "CISV";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachSystem [ "x86_64-linux" "aarch64-linux" ] (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pPkgs = pkgs.python313Packages;
      in
      {
        devShells.default = pkgs.mkShell {
          name = "CSCI";
          buildInputs = [
            pPkgs.uv
          ];
        };
      }
    );
}
