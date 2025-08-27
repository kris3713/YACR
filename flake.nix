{
  description = "A flake for development and GitHub Actions";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs =
    {
      self,
      nixpkgs
    }:

    let
      system = "x86_64-linux";
      legacyPackages = nixpkgs.legacyPackages;
      pkgs = legacyPackages.${system};
    in
    {
      # Define a devShell that provides all the required tools
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          # rpm
          python3
          fd
          sd
          ripgrep
          fish
        ];
      };
    };
}
