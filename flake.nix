{
  description = "A flake for development and GitHub Actions";

  inputs = {
    nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/0.1.*";
  };

  outputs =
    {
      self,
      nixpkgs
    }:

    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      # Define a devShell that provides all the required tools
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          fish
          fd
          # jq
          python3
          pixi
          sd
          ripgrep
          # yq-go
        ];
      };
    };
}
