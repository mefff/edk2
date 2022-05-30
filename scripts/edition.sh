#!/bin/bash

set -e

output_dir="${1:?}"
module_name="${2:?}"

edition=$(
    ar tf "${output_dir}/${module_name}.lib" | while read -a obj; do
	cat "${output_dir}/${obj[@]}.src"
	cat <(tr ' ' '\n' < "${output_dir}/headers.txt")
    done | \
	sort | \
	tee "log/${module_name}.files" | \
	xargs cat | \
	sha256sum | \
	cut -d' ' -f 1
    )

cat <<EOF > "${output_dir}/${module_name}.ini"
[uSWID]
edition = ${edition}
EOF

