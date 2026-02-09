# Grok Image Analyzer - ComfyUI Custom Node

A ComfyUI custom node that analyzes images using XAI's Grok vision model and generates detailed prompts suitable for image generation models.

## Features

- 🖼️ Analyzes images using Grok's vision capabilities
- 🎨 Generates detailed, structured prompts for image generation
- ⚙️ Configurable system and user prompts
- 🔒 Secure API key handling (supports environment variables)
- 🚀 Fast inference with non-reasoning Grok model

## Installation

### Option 1: Direct Installation to ComfyUI

1. Copy the `comfyui_grok_image_analyzer.py` file to your ComfyUI `custom_nodes` directory:

```bash
cp comfyui_grok_image_analyzer.py /path/to/ComfyUI/custom_nodes/
```

2. Install required Python packages (if not already installed):

```bash
pip install requests pillow
```

### Option 2: As a Git Submodule

```bash
cd /path/to/ComfyUI/custom_nodes
git submodule add <this-repo-url> grok-analyzer
```

## Setup

### 1. Get Your API Key

- Sign up at [x.ai](https://x.ai) (formerly XAI)
- Get your API key from the dashboard
- Keep it secure!

### 2. Configure API Key

You can provide the API key in two ways:

**Option A: Environment Variable (Recommended)**

```bash
export XAI_API_KEY="your-api-key-here"
```

**Option B: Node Input**
Simply paste your API key directly into the node's `api_key` input field in ComfyUI.

### 3. Optional: Configure Base URL

If using a custom API endpoint, set:

```bash
export XAI_BASE_URL="https://custom-api.example.com/v1"
```

## Node Inputs

| Input           | Type     | Description                  | Default                                     |
| --------------- | -------- | ---------------------------- | ------------------------------------------- |
| `image`         | IMAGE    | Input image to analyze       | Required                                    |
| `api_key`       | STRING   | XAI API key (or use env var) | ""                                          |
| `model`         | DROPDOWN | Model to use                 | `grok-4-1-fast-non-reasoning`               |
| `user_prompt`   | STRING   | Analysis instructions        | "Describe this image in detail..."          |
| `system_prompt` | STRING   | System context (optional)    | "You are an expert at creating detailed..." |

## Node Outputs

| Output   | Type   | Description                  |
| -------- | ------ | ---------------------------- |
| `prompt` | STRING | Generated descriptive prompt |

## Usage Examples

### Basic Image Captioning

1. Load an image with your image loader node
2. Add the **Grok Image Analyzer** node
3. Connect the image to the node
4. Add your API key
5. Run the workflow
6. Use the output prompt in your image generation node

### Custom Analysis Prompts

For specific use cases, customize the prompts:

**For Product Photography:**

```
user_prompt: "Generate a detailed product description prompt suitable for a professional product image generation model. Include materials, textures, lighting, and styling."
```

**For Character Design:**

```
user_prompt: "Create a detailed character description in a format suitable for character design prompts. Include appearance, clothing, style, and mood."
```

**For Landscape Analysis:**

```
user_prompt: "Describe this landscape with focus on geographical features, climate indicators, time of day, and environmental details useful for landscape generation."
```

## Workflow Integration

Common workflow pattern:

```
Image Loader
    ↓
Grok Image Analyzer → Prompt Output
    ↓
Image Generation Model (e.g., Stable Diffusion)
    ↓
Output Image
```

## Troubleshooting

### "API key not provided"

- Check that `XAI_API_KEY` environment variable is set, or
- Paste the API key directly in the node's `api_key` field

### "No analysis returned from Grok"

- Check that your API key is valid
- Ensure you have sufficient API quota
- Verify the image is a valid format (PNG, JPG, WebP, GIF)

### Connection timeout

- Check your internet connection
- Verify the API base URL is correct
- Try increasing timeout in the node code if needed

### CORS or SSL errors

- Ensure you're not behind a proxy that's interfering
- Check that your firewall allows HTTPS requests to api.x.ai

## API Model Options

Currently available Grok models:

- `grok-4-1-fast-non-reasoning` - Fast, efficient model suitable for real-time analysis

For additional models, update the dropdown in the `INPUT_TYPES` method.

## Limitations

- **Max image size**: The API has limits on image resolution; very large images may need to be resized
- **Timeout**: API requests timeout after 60 seconds
- **Rate limiting**: Subject to XAI API rate limits (check your pricing plan)
- **Supported formats**: PNG, JPG, WebP, GIF

## Performance Tips

1. **Batch Processing**: Use the node sequentially for multiple images in different workflows
2. **Prompt Engineering**: Optimize your user_prompt for better, more specific outputs
3. **Model Choice**: `grok-4-1-fast-non-reasoning` is optimized for speed without reasoning overhead

## Related Resources

- [XAI Documentation](https://api.x.ai/documentation)
- [ComfyUI Documentation](https://github.com/comfyanonymous/ComfyUI)
- [Grok Vision Capabilities](https://x.ai/api/docs#vision)

## License

Same license as the parent project.

## Contributing

Found an issue or have a feature request? Please submit an issue in the repository.
