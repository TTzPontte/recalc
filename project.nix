{ 
  imports = [ ./event.nix ];
  config.files.gitignore.enable = true;
  config.files.gitignore.template.Python = true;
  config.files.cmds."nodePackages.serverless" = true;
  config.files.cmds.python39 = true;
}
