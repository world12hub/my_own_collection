#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Creates or updates a text file on the remote host

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: Creates a text file at the specified path with the specified content.

options:
    path:
        description: Path to the text file on the remote host.
        required: true
        type: path
    # new:
    #     description:
    #         - Control to demo if the result of this module is changed or not.
    #         - Parameter description can be a list as well.
    #     required: false
    #     type: bool
    content:
        description: Content to write to the text file.
        required: true
        type: str
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - my_namespace.my_collection.my_doc_fragment_name

author:
    - Sergey Kanyugin (@world12hub)
'''

EXAMPLES = r'''
# Pass in a message
- name: Create a text file
  my_namespace.my_collection.my_test:
    path: /tmp/example.txt
    content: "hello world\n"

# pass in a message and have changed true
- name: Update file content
  my_namespace.my_collection.my_test:
    path: /tmp/example.txt
    content: "new content"
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
path:
    description: Path to the file that was managed.
    type: str
    returned: always
    sample: /tmp/example.txt
message:
    description: Human-readable result message.
    type: str
    returned: always
    sample: 'File created/updated: /tmp/example.txt'
'''

from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='path', required=True),
        content=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        path='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    path = module.params['path']
    content = module.params['content']
    result['path'] = path

    changed = False

    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                old_content = f.read()
        except (OSError, IOError, UnicodeDecodeError) as e:
            module.fail_json(msg='Cannot read file %s: %s' % (path, e), **result)

        changed = old_content != content
    else:
        changed = True

    result['changed'] = changed
    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    if changed:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        except (OSError, IOError) as e:
            module.fail_json(msg='Cannot write file %s: %s' % (path, e), **result)

        result['message'] = 'File created/updated: %s' % path
    else:
        result['message'] = 'File already has requested content: %s' % path

    module.exit_json(**result)

def main():
    run_module()


if __name__ == '__main__':
    main()
