import asyncio
import sys
import aiohttp

PYPI_URL = "https://pypi.org/pypi/{}/json"

# Common module imports that map to different PyPI package names
PACKAGE_MAPPINGS = {
    "cv2": "opencv-python",
    "sklearn": "scikit-learn",
    "PIL": "Pillow",
    "yaml": "PyYAML",
    "bs4": "beautifulsoup4",
}


def filter_external_packages(imports: list[str]) -> list[str]:
    """Filters standard library modules and maps import aliases to canonical PyPI packages."""
    stdlib_modules = getattr(sys, "stdlib_module_names", set())
    external_packages = set()

    for imp in imports:
        if imp in stdlib_modules or imp.startswith("_"):
            continue
        pypi_name = PACKAGE_MAPPINGS.get(imp, imp)
        external_packages.add(pypi_name)

    return sorted(list(external_packages))


async def check_package(session: aiohttp.ClientSession, package: str) -> dict:
    url = PYPI_URL.format(package)
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=8)) as response:
            if response.status == 200:
                data = await response.json()
                return {
                    "package": package,
                    "exists": True,
                    "version": data.get("info", {}).get("version"),
                    "summary": data.get("info", {}).get("summary"),
                    "error": None
                }
            if response.status == 404:
                return {
                    "package": package,
                    "exists": False,
                    "version": None,
                    "summary": None,
                    "error": "Package does not exist on PyPI"
                }
            return {
                "package": package,
                "exists": None,
                "version": None,
                "summary": None,
                "error": f"HTTP {response.status}"
            }
    except asyncio.TimeoutError:
        return {
            "package": package,
            "exists": None,
            "version": None,
            "summary": None,
            "error": "Request timed out"
        }
    except Exception as exc:
        return {
            "package": package,
            "exists": None,
            "version": None,
            "summary": None,
            "error": str(exc)
        }


async def verify_packages(packages: list[str]) -> list[dict]:
    filtered_packages = filter_external_packages(packages)
    if not filtered_packages:
        return []

    async with aiohttp.ClientSession(headers={"User-Agent": "CodeSanitizer/1.0"}) as session:
        tasks = [check_package(session, pkg) for pkg in filtered_packages]
        return await asyncio.gather(*tasks)