{ pkgs ? import <nixpkgs> {} 
, pkgsLinux ? import <nixpkgs> { system = "x86_64-linux"; }
}:

let

  base = pkgs.dockerTools.pullImage {
    imageName = "docker.io/lcsavb/autocusto-base-image";
    sha256 = "sha256-orLq7d1VuVhioZpN4MFHZkk9SipjS5/N61penY7nTNo=";
    imageDigest = "sha256:3ceed35ade29d4b02dea8e1135b4c07d1ca3d481497e011695c964ac9c283d9b";
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

  pythonEnv = pkgs.python311.withPackages (ps: with ps; [
    django
    django_extensions
    django-crispy-forms
    django-crispy-bootstrap4
    pypdftk
  ]);

in

pkgs.dockerTools.buildImage {
  name = "ac2";
  tag = "dev";
  fromImage = base;
  contents = [
    pythonEnv
    pkgs.bash
    pkgs.coreutils
  ];

  runAsRoot = ''
    mkdir -p /app
    cp -r ${./.}/* /app/
    chmod +x /app/startup.sh
  '';

  config = {    
    WorkingDir = "/app";
    ExposedPorts = {
      "8000/tcp" = {};
    };
    Cmd = [ "/bin/sh" "-c" 
    "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000" 
    ];   
  };

}