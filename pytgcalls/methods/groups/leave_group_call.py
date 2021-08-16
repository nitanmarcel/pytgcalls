import asyncio

from ...exceptions import PyrogramNotSet, NodeJSNotRunning, NoActiveVoiceChat
from ...scaffold import Scaffold


class LeaveGroupCall(Scaffold):
    async def leave_group_call(
        self,
        chat_id: int,
    ):
        if self._app is not None:
            if self._binding.is_alive() or \
                    self._wait_until_run is not None:
                chat_call = await self._full_chat_cache.get_full_chat(
                    chat_id,
                )
                if chat_call is not None:
                    async def internal_sender():
                        await self._wait_until_run.wait()
                        await asyncio.sleep(0.06)
                        await self._binding.send({
                            'action': 'leave_call',
                            'chat_id': chat_id,
                            'type': 'requested',
                        })
                    asyncio.ensure_future(internal_sender())
                else:
                    raise NoActiveVoiceChat()
            else:
                raise NodeJSNotRunning()
        else:
            raise PyrogramNotSet()
