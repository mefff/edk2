#!/bin/bash

set -e

output_dir="${1:?}"
module_name="${2:?}"

sources_list="$(ar tf "${output_dir}/${module_name}.lib" | while read -a obj; do
		   cat "${output_dir}/${obj[@]}.src"
	       done)"

headers_list="$(tr ' ' '\n' < ${output_dir}/headers.txt)"

files_list="$(printf "%s\n%s" "$sources_list" "$headers_list")"

edition="$(echo $files_list | \
	      sort | \
	      tee "${module_name}.files" | \
	      xargs cat | \
	      sha256sum | \
	      cut -d' ' -f 1)"

cat <<EOF > "${output_dir}/${module_name}.ini"
[uSWID]
edition = ${edition}
EOF

