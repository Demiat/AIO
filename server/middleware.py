import json
import logging

from aiohttp import web


logger = logging.getLogger("request")


@web.middleware
async def request_logging_middleware(request, handler):
    max_log_body_bytes = 10_000
    log_data = {
        "remote_addr": request.remote,
        "method": request.method,
        "path": str(request.rel_url),
        "request_body": None,
        "query_string": str(request.query_string),
        "user_agent": request.headers.get("User-Agent"),
        "content_length": request.content_length,
        "status": None,
        "response_body": None,
    }

    try:
        if (
            request.can_read_body
            and request.content_type == "application/json"
            and request.content_length is not None
            and request.content_length <= 10_000  # 10 КБ
        ):
            body = await request.read()
            log_data["request_body"] = json.loads(body.decode("utf-8")) if body else {}
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.exception("Error reading request body: %s", e)
    except Exception:
        pass

    try:
        response = await handler(request)
        log_data["status"] = response.status
        try:
            response_text = getattr(response, "text", None)
            if isinstance(response_text, str):
                log_data["response_body"] = response_text[:100]
        except Exception:
            pass
        return response

    except web.HTTPException as e:
        log_data["status"] = e.status
        log_data["error"] = e.reason
        return web.json_response(
            {"error": e.reason},
            status=e.status
        )

    except Exception as e:
        log_data["status"] = 500
        log_data["error"] = str(e)
        return web.json_response(
            {"error": "Internal server error"},
            status=500
        )

    finally:
        status = log_data.get("status")
        if status is None:
            logger.warning(msg=log_data)
        elif status >= 500:
            logger.error(msg=log_data)
        elif status >= 400:
            logger.warning(msg=log_data)
        else:
            logger.info(msg=log_data)
