{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = import nixpkgs { inherit system; }; in {
        devShells.default = pkgs.mkShell { buildInputs = [
          pkgs.texlive.combined.scheme-full
        ]; };
      });
}

