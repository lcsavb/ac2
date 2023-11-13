{ pkgs ? import <nixpkgs> {} 
, pkgsLinux ? import <nixpkgs> { system = "x86_64-linux"; }
}:


let
    currentDir = ./.;
    
    nixFromDockerHub = pkgs.dockerTools.pullImage {
    imageName = "nixos/nix";
    imageDigest = "sha256:85299d86263a3059cf19f419f9d286cc9f06d3c13146a8ebbb21b3437f598357";
    sha256 = "19fw0n3wmddahzr20mhdqv6jkjn1kanh6n2mrr08ai53dr8ph5n7";
    finalImageTag = "2.2.1";
    finalImageName = "nix";
  };

    pypdftk = pkgs.python3Packages.buildPythonPackage rec {
    pname = "pypdftk";
    version = "0.5";
    src = pkgs.python3Packages.fetchPypi {
      inherit pname version;
      sha256 = "sha256-tvfwABM0gIQrO/n4Iiy2vV4rIM9QxewFDy5E2ffcMpY";

    };
    doCheck = false;
  };

    pythonEnv = pkgs.python311.withPackages (ps: [
      ps.pip
      ps.django
      pypdftk
  ]);

in

pkgs.dockerTools.buildImage {
  name = "ac2";
  tag = "dev";
  fromImage = nixFromDockerHub;
  contents = [ 
	currentDir
	pkgs.bash
	pythonEnv
	pkgs.pdftk
];
  config = {
    Cmd = [ "/bin/sh" "-c" "./startup.sh" ];    
      ExposedPorts = {
      "8000/tcp" = {};
    };
  };


}
