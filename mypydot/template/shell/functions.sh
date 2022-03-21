function test_dotfiles() {
  echo "Hello world"
}

function measure_performance_shell() {
  # shellcheck disable=SC2034
  for i in $(seq 1 10); do time zsh -i -c exit; done
}
