import { useMutation } from '@tanstack/react-query'
import { useState, useEffect } from 'react'
import { Toaster, toast } from 'sonner'

interface Payload {
    url: string
}

export const App = () => {
    const [text, setText] = useState<string>('')
    const [redirectState, setRedirectState] = useState<string>('')

    const minifyMutation = useMutation<Payload, Error>({
        mutationKey: ['minifyMutation'],
        mutationFn: async () => {
            const output = await fetch('http://127.0.0.1:8000/minify_url',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        url: text
                    })
                }
            ).then( async (res) => res.json())
            return output
        }})

    const redirectMutation = useMutation<void, Error>({
        mutationKey: ['redirectMutation'],
        mutationFn: async () => {
            window.location.href = `http://127.0.0.1:8000/${redirectState}`
        }
    })

    const minifyUrl = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const output = await minifyMutation.mutateAsync()
        console.log(`output url: ${output.url}`)
        return output
    }

    const redirectUrl = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        return await redirectMutation.mutate()
    }

    return (
        <div>
            <form id="min-form" onSubmit={async (e: React.FormEvent<HTMLFormElement>) => {
                const output = await minifyUrl(e)
                toast("Compressed URL created", {
                    description: output.url,
                    duration: 3000
                })
            }}>
                <label id="url-one"> Minify URL </label> <br/>
                <input id="url-one" type="text" onChange={(e) => setText(e.target.value)}/>
                <button type="submit"> Submit </button>
            </form>
            <form id="rev-navigate" onSubmit={redirectUrl}>
                <label id="url-two"> Redirect Form</label> <br/>
                <input id="url-two" type="text" onChange={(e) => setRedirectState(e.target.value)}/>
                <button type="submit"> Submit </button>
            </form>
        </div>
    )
}
