{
  description = "A very basic flake";

  inputs.mach-nix.url = "github:davhau/mach-nix";
  outputs = {self, mach-nix}: {
    packages.x86_64-linux.default = mach-nix.lib.x86_64-linux.buildPythonApplication {
      pname = "lithekod-website";
      version = "0.1.0";
      src = ./.;
      requirements = builtins.readFile ./requirements.txt;
    };
    devShells.x86_64-linux.default = mach-nix.lib.x86_64-linux.mkPythonShell {
      requirements = builtins.readFile ./requirements.txt;
    };
  };
}
