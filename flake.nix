{
  description = "Dev Environment";

  inputs.dsf.url = "github:cruel-intentions/devshell-files";
  inputs.gha.url = "github:cruel-intentions/gh-actions";
  inputs.pontix.url = "git+ssh://git@github.com/pontte/pontix.git";

  outputs = inputs: inputs.dsf.lib.mkShell [
    "${inputs.gha}/gh-actions.nix"
    "${inputs.pontix}/modules/aws.nix"
    "${inputs.pontix}/modules/cache-s3.nix"
    "${inputs.pontix}/modules/git.nix"
    "${inputs.pontix}/modules/notify-slack.nix"
    ./project.nix
  ];
}
