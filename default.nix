{ pkgs ? import <nixpkgs> {} }:

let
  # Custom packages
  pypdftk = pkgs.python3Packages.buildPythonPackage rec {
    pname = "pypdftk";
    version = "0.5";
    src = pkgs.python3Packages.fetchPypi {
      inherit pname version;
      sha256 = "sha256-tvfwABM0gIQrO/n4Iiy2vV4rIM9QxewFDy5E2ffcMpY";

    };
    doCheck = false;
  };
in
pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pypdftk 
    pkgs.python3Packages.django
    pkgs.python3Packages.django-extensions
    pkgs.pdftk
  ];
}
