from fastapi import APIRouter 
from schemas.QnA import ChatbotRequest
from services.QnA import get_chatbot_response

router = APIRouter()

@router.post("/chatbot")
async def chatbot_endpoint(query: ChatbotRequest):
    try:
        responseText = await get_chatbot_response(query)
        return {
            "response": responseText,
        }
    except Exception as e:
        return {
            "response": f"error occured",
        }

