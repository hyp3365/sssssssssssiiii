# bandwidth-limiter

`bandwidth-limiter` outbound ported from
[shtorm-7/sing-box-extended](https://github.com/shtorm-7/sing-box-extended)
(`protocol/limiter/bandwidth`, commit 5956780) to official SagerNet/sing-box.

`build-xhttp.yml` runs `apply.py` inside the official sing-box tree before building.

Changes vs. upstream:
- `route.NewRouter` call adapted to the official signature (no name argument)
- removed `hwid` / `mux` connection types and flow keys (not available in official sing-box)
- removed `manager` strategy (needs extended's manager service)
- fix: `users` strategy now uses each user's own `speed` (upstream used the top-level speed)
- missing `speed` returns a config error instead of panicking

## Options

- `strategy`: `global` | `connection` | `users` | `bypass`
- `mode`: `upload` | `download` | `bidirectional`
- `connection_type` (connection strategy): `default` | `source_ip`
- `flow_keys` (fair queue inside one limit): `user` | `source_ip` | `protocol` | `destination`
- `speed`: e.g. `100KB`, `5MB`
- `route`: nested route (`rules`, `final`) used after limiting

Per inbound: route rule `{"inbound": ["tag"], "outbound": "<global limiter>"}`.
Per user: route rule `{"auth_user": ["name"], "outbound": "<users limiter>"}`.
See `example.json`.
