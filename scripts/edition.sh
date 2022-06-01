#!/bin/bash

set -xe -o pipefail

output_dir="${1:?}"
module_name="${2:?}"


sources_list="$(while read -a obj; do
		    cat ${obj}.src
		done < ${output_dir}/object_files.lst)"

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

