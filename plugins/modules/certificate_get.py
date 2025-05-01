#!/usr/bin/python
__metaclass__ = type

# Manage TrueNAS certificates

DOCUMENTATION = '''
---
module: certificate_query
short_description: Query TrueNAS certificates
description:
  - Interact with the TrueNAS API to query certificates.
options:
  query_filter:
    description:
      - A filter to apply to the query. This should be a list of conditions
        to filter the certificates.
    type: list
    elements: list
  query_options:
    description:
      - Additional options for the query, such as sorting or limiting results.
    type: dict
version_added: "1.10.1"
'''

EXAMPLES = '''
- name: Query all certificates
  hosts: my-truenas-host
  tasks:
    - name: Get certificates
      arensb.truenas.certificate_query:
        query_filter: []
        query_options: {}
'''

RETURN = '''
certificates:
  description: A list of certificates returned by the query.
  type: list
  returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.arensb.truenas.plugins.module_utils.middleware \
    import MiddleWare as MW


def main():
    module = AnsibleModule(
        argument_spec=dict(
            query_filter=dict(type='list', elements='list', default=[]),
            query_options=dict(type='dict', default={}),
        ),
        supports_check_mode=True,
    )

    result = dict(
        changed=False,
        certificates=[]
    )

    mw = MW.client()

    # Assign variables from properties
    query_filter = module.params['query_filter']
    query_options = module.params['query_options']

    # Query the certificates
    try:
        certificates = mw.call("certificate.query", query_filter, query_options)
        result['certificates'] = certificates
    except Exception as e:
        module.fail_json(msg=f"Error querying certificates: {e}")

    module.exit_json(**result)


# Main
if __name__ == "__main__":
    main()