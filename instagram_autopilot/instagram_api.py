import requests
import config


class InstagramAPI:
    """Wrapper for the Instagram Graph API."""

    def __init__(self):
        self.account_id = config.INSTAGRAM_ACCOUNT_ID
        self.token = config.INSTAGRAM_ACCESS_TOKEN
        self.base = config.INSTAGRAM_GRAPH_URL

    def _get(self, endpoint: str, params: dict = None) -> dict:
        params = params or {}
        params["access_token"] = self.token
        resp = requests.get(f"{self.base}/{endpoint}", params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def _post(self, endpoint: str, data: dict) -> dict:
        data["access_token"] = self.token
        resp = requests.post(f"{self.base}/{endpoint}", data=data, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_account_info(self) -> dict:
        """Fetch basic account info to verify credentials."""
        return self._get(
            self.account_id,
            {"fields": "id,username,followers_count,media_count"},
        )

    def create_image_container(self, image_url: str, caption: str) -> str:
        """
        Step 1: Upload media container.
        image_url must be a publicly accessible HTTPS URL.
        Returns container_id.
        """
        result = self._post(
            f"{self.account_id}/media",
            {"image_url": image_url, "caption": caption},
        )
        return result["id"]

    def publish_container(self, container_id: str) -> str:
        """
        Step 2: Publish the media container.
        Returns the published media id.
        """
        result = self._post(
            f"{self.account_id}/media_publish",
            {"creation_id": container_id},
        )
        return result["id"]

    def post_image(self, image_url: str, caption: str) -> dict:
        """
        Full two-step publish flow.
        Returns {"container_id": str, "media_id": str, "success": bool}
        """
        container_id = self.create_image_container(image_url, caption)
        media_id = self.publish_container(container_id)
        return {
            "container_id": container_id,
            "media_id": media_id,
            "success": True,
        }

    def create_carousel_container(self, image_urls: list[str], caption: str) -> str:
        """Post a carousel (up to 10 images). Returns container_id."""
        children = []
        for url in image_urls[:10]:
            result = self._post(
                f"{self.account_id}/media",
                {"image_url": url, "is_carousel_item": "true"},
            )
            children.append(result["id"])

        result = self._post(
            f"{self.account_id}/media",
            {
                "media_type": "CAROUSEL",
                "children": ",".join(children),
                "caption": caption,
            },
        )
        return result["id"]

    def get_recent_media(self, limit: int = 10) -> list:
        """Fetch recent posts for monitoring."""
        result = self._get(
            f"{self.account_id}/media",
            {"fields": "id,caption,timestamp,like_count,comments_count", "limit": limit},
        )
        return result.get("data", [])
