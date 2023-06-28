import os
from typing import Union, List, Literal

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

import g4f

PROVIDERS = [
    # 'Ails',
    # 'You',
    # 'Bing',
    'Yqcloud',
    # 'Theb',
    # 'Aichat',
    # 'Bard',
    # 'Vercel',
    'Forefront',
    'Lockchat',
    # 'Liaobots',
    # 'H2o',
    'ChatgptLogin',
    # 'DeepAi',
    # 'GetGpt',
]

MODELS = [
    'gpt-3.5-turbo',
    'gpt-4',
]

AUTH_TOKEN = os.getenv('TOKEN', '')
app = FastAPI()


class Message(BaseModel):
    role: Literal['user', 'assistant', 'system']
    content: str


class Args(BaseModel):
    messages: List[Message]
    model: Union[str, None] = 'gpt-3.5-turbo'
    provider: Union[str, None] = 'Forefront'


def auth_by_token(token: str):
    if not AUTH_TOKEN:
        return
    if token == AUTH_TOKEN:
        return
    raise HTTPException(status_code=403)


@app.post('/gpt/chat')
def gpt_chat(args: Args, token: str = Header(None)):
    auth_by_token(token)
    if args.model not in MODELS:
        raise HTTPException(status_code=400, detail=f'Invalid model: {args.model=}, {MODELS=}')
    if args.provider not in PROVIDERS:
        raise HTTPException(status_code=400, detail=f'Invalid provider: {args.provider=}, {PROVIDERS=}')
    res = g4f.ChatCompletion.create(
        model=args.model, provider=getattr(g4f.Provider, args.provider),
        messages=[m.dict() for m in args.messages], stream=False)
    return {'code': 200, 'provider': args.provider, 'msg': res}


if __name__ == '__main__':
    try:
        response = g4f.ChatCompletion.create(
            model='gpt-3.5-turbo', provider=getattr(g4f.Provider, 'Forefront'),
            messages=[
                {"role": "user", "content": "Hello world"}], stream=False)
        print(response)
    except Exception as e:
        print(f'An error occurred: {e}')
