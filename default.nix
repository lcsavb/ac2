{ pkgs ? import <nixpkgs> {} 
, pkgsLinux ? import <nixpkgs> { system = "x86_64-linux"; }
}:

let
  dockerTools = pkgs.dockerTools;
  currentDir = ./.;
  pythonTiny = dockerTools.pullImage {
    imageName = "docker.io/lcsavb/python-tiny";
    sha256 = "sha256-lPenxSMmed8Ab+jy9en2UaMnBcCYlR1/CYOxh8M0htk=";
    imageDigest = "sha256:9d5d8fc0f7592c64c23d4028a7acc9e8a46bb5789620368cd917124f06e4eaf9";
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

  crispyForms = pkgs.python3Packages.buildPythonApplication rec {
    pname = "django-crispy-forms";
    version = "2.1";  # use the version you need

    src = pkgs.python3Packages.fetchPypi {
      inherit pname version;
      sha256 = "sha256-TX7EMZM61NS1xabeSlhNJGE8NH25rBaHI8mq9jr0u5Y=";  # replace with the correct sha256
    };

    format = "pyproject";

    doCheck = false;
  };

  pythonEnv = pkgs.python311.withPackages (ps: [
    ps.pip
    ps.django
    ps.django_extensions
    crispyForms
    pypdftk
  ]);
in
pkgs.dockerTools.buildImage {
  name = "ac2";
  tag = "dev";
  fromImage = pythonTiny;
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