#!/bin/bash

set -xe -o pipefail

output_dir="${1:?}"
module_name="${2:?}"

edition="$(cat "${output_dir}/source_files.lst" "${output_dir}/header_files.lst" | \
	      tr ' ' '\n' | \
	      sort -u | \
	      tee "${module_name}.files" | \
	      xargs cat | \
	      sha256sum | \
	      cut -d' ' -f 1)"

echo "${module_name} | ${edition}"

cat <<EOF > "${output_dir}/${module_name}.ini"
[uSWID]
edition = ${edition}
EOF

