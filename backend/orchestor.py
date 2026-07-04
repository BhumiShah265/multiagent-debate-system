import json
import asyncio
from sqlalchemy.orm import Session
import models
import schemas
from agents import generate_argument, evaluate_round,determine_winner_and_final_positioins 
def format_sse(event:str, data:dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"

async def run_debate_loop(
    debate_id:int,
    db:Session,
    optimist_model:str,
    skeptic_model:str,
    realist_model:str,
    referee_model:str):

    try:
        debate = db.query(models.Debate).filter(models.Debate.id == debate_id).first()

        if not debate:
            yield format_sse("error",{"message":"Debate session not found"})
            return
        
        debate.status = models.DebateStatus.RUNNING
        db.commit()
        

        agent_configs = [
            {"name":"Aura (OPTIMIST)","persona":models.PersonaType.OPTIMIST,"model":optimist_model},
            {"name": "Socrates (Skeptic)", "persona": models.PersonaType.SKEPTIC, "model": skeptic_model},
            {"name": "Sophia (Realist)", "persona": models.PersonaType.REALIST, "model": realist_model}
        ]
        db_agents = []
        for config in agent_configs:
            agent = db.query(models.DebateAgent).filter(
                models.DebateAgent.debate_id == debate_id,
                models.DebateAgent.name == config['name']
            ).first()

            if not agent:
                agent = models.DebateAgent(
                    debate_id = debate_id,
                    name = config['name'],
                    persona = config['persona'],
                    model_name = config['model']
                )
                db.add(agent)
                db.flush()
            db_agents.append(agent)
        db.commit()
        agents_data = [
            {"id":a.id,"name":a.name,"persona":a.persona,"model":config["model"]}
            for a, config in zip(db_agents,agent_configs)
        ]
        yield format_sse("debate_started",{
             "debate_id": debate.id,
            "topic": debate.topic,
            "rounds_count": debate.rounds_count,
            "agents": agents_data
        })
        await asyncio.sleep(1) # Small pause for UI effect
    except Exception as e:
        db.rollback()
        # Set status to FAILED on error
        debate = db.query(models.Debate).filter(models.Debate.id == debate_id).first()
        if debate:
            debate.status = models.DebateStatus.FAILED
            db.commit()
        yield format_sse("error", {"message": str(e)})