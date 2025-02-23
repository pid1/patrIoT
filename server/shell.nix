{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.python312Packages.openai
    pkgs.python312Packages.pillow
    pkgs.python312Packages.requests
  ];

}