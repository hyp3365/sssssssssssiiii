package option

import "github.com/sagernet/sing/common/byteformats"

type BandwidthLimiterOutboundOptions struct {
	Strategy       string                          `json:"strategy"`
	ConnectionType string                          `json:"connection_type,omitempty"`
	Mode           string                          `json:"mode"`
	FlowKeys       []string                        `json:"flow_keys,omitempty"`
	Speed          *byteformats.NetworkBytesCompat `json:"speed,omitempty"`
	Users          []BandwidthLimiterUser          `json:"users,omitempty"`
	Route          RouteOptions                    `json:"route"`
}

type BandwidthLimiterUser struct {
	Name           string                          `json:"name"`
	Strategy       string                          `json:"strategy"`
	ConnectionType string                          `json:"connection_type,omitempty"`
	Mode           string                          `json:"mode"`
	Speed          *byteformats.NetworkBytesCompat `json:"speed"`
}
