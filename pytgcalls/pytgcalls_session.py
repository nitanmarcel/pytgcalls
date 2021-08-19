import re
import sys

import httpx
from httpx import Response

from .__version__ import __version__
from .version_manager import VersionManager


class PyTgCallsSession:
    notice_displayed = False

    async def start(self):
        if not self.notice_displayed:
            PyTgCallsSession.notice_displayed = True
            print(
                f'PyTgCalls v{__version__}, Copyright (C) '
                f'2021 Laky-64 <https://github.com/Laky-64>\n'
                'Licensed under the terms of the GNU Lesser '
                'General Public License v3 or later (LGPLv3+)\n',
            )
            remote_stable_ver = await self._remote_version('master')
            remote_dev_ver = await self._remote_version('dev')
            if VersionManager.version_tuple(__version__) > \
                    VersionManager.version_tuple(remote_stable_ver + '.99'):
                remote_ver = remote_readable_ver = remote_dev_ver
                my_ver = __version__
            else:
                remote_readable_ver = remote_stable_ver
                remote_ver = remote_stable_ver + '.99'
                my_ver = __version__ + '.99'
            if VersionManager.version_tuple(remote_ver) > \
                    VersionManager.version_tuple(my_ver):
                text = f'Update Available!\n'\
                       f'New PyTgCalls v{remote_readable_ver} ' \
                       f'is now available!\n'
                if sys.platform.startswith('win'):
                    print(f'\033[93m{text}\033[0m')
                else:
                    print(text)

    @staticmethod
    async def _remote_version(branch: str):
        async def get_async(url) -> Response:
            async with httpx.AsyncClient(http2=True) as client:
                return await client.get(url)
        return re.findall(
            '__version__ = \'(.*?)\'', (
                await get_async(
                    f'https://raw.githubusercontent.com/'
                    f'pytgcalls/pytgcalls/{branch}'
                    f'/pytgcalls/__version__.py',
                )
            ).text,
        )[0]
