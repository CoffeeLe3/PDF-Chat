export async function GET(req: Request) {
    const { searchParams } = new URL(req.url)
    const filename = searchParams.get("filename")

    const res = await fetch(`http://localhost:8000/pdf/generate-upload-url?filename=${filename}`)
    const data = await res.json()
    return new Response(JSON.stringify(data))
}