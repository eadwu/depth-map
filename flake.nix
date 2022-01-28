{
  description = "depth-map";

  # General Repositories
  inputs.nixpkgs = { type = "github"; owner = "NixOS"; repo = "nixpkgs"; ref = "nixos-21.05"; };
  inputs.flake-compat = { type = "github"; owner = "edolstra"; repo = "flake-compat"; flake = false; };

  # Reproducible Python Environments
  inputs.mach-nix = { type = "github"; owner = "DavHau"; repo = "mach-nix"; flake = false; };

  outputs = { self, nixpkgs, ... }@inputs:
    let
      supportedSystems = [ "x86_64-linux" ];
      forAllSystems = f: nixpkgs.lib.genAttrs supportedSystems (system: f system);

      config = { allowUnfree = true; };
      nixpkgsFor = forAllSystems (system: import nixpkgs { inherit config system; overlays = [ self.overlay ]; });
    in
    {

      overlay = final: prev:
        with final; {

          # cudatoolkit = final.cudatoolkit_10_1;
          # cudnn = final.cudnn_cudatoolkit_10_1;
          # nccl = prev.nccl.override { cudatoolkit = final.cudatoolkit_10_1; };

        };

      devShell = forAllSystems (system:
        let
          pkgs = nixpkgsFor.${system};
          mach-nix = import inputs.mach-nix {
            inherit pkgs;
            python = "python39";

            # Latest dependency resolution chain as of `JJan 19 20:32:51 UTC 2022`
            pypiDataRev = "fb1208ad9edad2acd42f5f9c5ac8035518b4fdd7";
            pypiDataSha256 = "1w1sbf295rd7s4258a79zgwq499whwx2bmisy93cv1n0ir5l5j1l";
          };

          env = mach-nix.mkPython
            rec {
              requirements = ''
                timm
                tqdm
                numpy
                scipy
                pandas
                sklearn

                # Visualization
                matplotlib

                # Computer Vision
                piqa
                pillow
                opencv-python

                # PyTorch
                torch
                torchvision
                torchaudio
                tensorboard

                torchinfo

                # Jupyter
                jupyterlab
                notebook
                voila
              '';

              providers = {
                # _default = "conda-forge,conda,wheel,sdist,nixpkgs";
                _default = "wheel,sdist,nixpkgs";
                # jupyterlab = "conda-forge";
                # voila = "conda-forge";
              };

              # _.torch.src = pkgs.fetchurl {
              #   name = "torch-1.9.0+cu111-cp39-cp39-linux_x86_64.whl";
              #   url = "https://download.pytorch.org/whl/cu111/torch-1.9.0%2Bcu111-cp39-cp39-linux_x86_64.whl";
              #   sha256 = "VCLRkELiF8KqlAMLFrP+TaW+m6jupG5+WdQKEQlVli0=";
              # };

              # _.torchvision.src = pkgs.fetchurl {
              #   name = "torchvision-0.10.0+cu111-cp39-cp39-linux_x86_64.whl";
              #   url = "https://download.pytorch.org/whl/cu111/torchvision-0.10.0%2Bcu111-cp39-cp39-linux_x86_64.whl";
              #   sha256 = "AOfhnHThVdJx5qxj2LTj+T9dPMFxQoxP3duxIm1y7KE=";
              # };

              # _.torchaudio.src = pkgs.fetchurl {
              #   url = "https://download.pytorch.org/whl/torchaudio-0.9.0-cp39-cp39-linux_x86_64.whl";
              #   sha256 = "718LImRqlPlYaQAbQKuUBGixrjmdD/07xz1cQzQqATo=";
              # };
            };
        in
        pkgs.mkShell {
          buildInputs = [ env ];

          # Direnv (Lorri) Support
          PYTHON_ENV = env.out;
        });

    };
}
