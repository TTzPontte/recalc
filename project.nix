{ config, ...}:
{
  imports = [ ./event.nix ];
  config.files.gitignore.enable = true;
  config.files.gitignore.template.Python = true;
  config.files.cmds."nodePackages.serverless" = true;
  config.files.cmds.python39 = true;
  config.files.alias.deploy = ''
    STAGE=$(get-stage)
    sls deploy -s $STAGE
  '';
  config.gh-actions.ci-cd.enable = true;
  config.gh-actions.ci-cd.on.push.branches = ["master" "staging"];
  config.gh-actions.ci-cd.on.push.paths = ["src/**"];
  config.gh-actions.ci-cd.ssh-secret-name = "GH_ACTIONS_SSH_KEY";
  config.gh-actions.ci-cd.env.deploy = config.pontix.aws.ci-cd.envs;
  config.gh-actions.ci-cd.deploy = ''
    STAGE=$(get-stage)
    sls print -s $STAGE > sls_cfg.lock
    use-cache sls_cfg.lock ./
    deploy
    cache-it sls_cfg.lock .serverless
  '';
  config.gh-actions.ci-cd.post-deploy = "tag-it";
  config.gh-actions.notify-slack.enable = true;
  config.gh-actions.notify-slack.on.push.branches = ["master" "staging"];
  config.gh-actions.notify-slack.ssh-secret-name = "GH_ACTIONS_SSH_KEY";
}
