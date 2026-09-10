check_command() {
    local command="$1"

    command -v "$command" &>/dev/null
}

spawn() {
    (exec "$@" &>/dev/null &)
}

[[ -x "/opt/Lorien_v0.6.0_Linux/Lorien.x86_64" ]] && lorien() {
    spawn /opt/Lorien_v0.6.0_Linux/Lorien.x86_64
}
