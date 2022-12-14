from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.__all_models import *
from schemas.__all_schemas import *
from core.deps import get_session

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED,
            response_model=BetSchema)
async def post_bet(bet: BetSchema,
                    db: AsyncSession = Depends(get_session)):
    new_bet = BetModel(firstTeam= bet.firstTeam, 
    secondTeam= bet.secondTeam, firstTeamQuantyGoals= bet.firstTeamQuantyGoals,
    secondTeamQuantyGoals= bet.secondTeamQuantyGoals, user=bet.user)

    db.add(new_bet)
    await db.commit()
    return new_bet

@router.get('/', response_model=List[BetSchema],
            status_code=status.HTTP_200_OK)
async def get_bets(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(BetModel)
        result = await session.execute(query)
        bets: List[BetModel] = result.scalars().all()
        return bets

@router.get('/{bet_id}', 
            response_model=BetSchema, 
            status_code=status.HTTP_200_OK)
async def get_bet(bet_id: int, 
                    db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(BetModel).filter(BetModel.id == bet_id)
        result = await session.execute(query)
        bet = result.scalar_one_or_none()
        if bet:
            return bet
        else:
            raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Aposta não encontrada..."))

@router.put('/{bet_id}', 
            response_model=BetSchema, 
            status_code=status.HTTP_202_ACCEPTED)
async def put_bet(bet_id: int, bet: BetSchema,
                    db: AsyncSession = Depends(get_session)):
    pass
    async with db as session:
        query = select(BetModel).filter(BetModel.id == bet_id)
        result = await session.execute(query)
        bet_up = result.scalar_one_or_none()
        if bet_up:
            bet_up.firstTeam= bet.firstTeam, 
            bet_up.secondTeam= bet.secondTeam, 
            bet_up.firstTeamQuantyGoals= bet.firstTeamQuantyGoals,
            bet_up.secondTeamQuantyGoals= bet.secondTeamQuantyGoals, 
            bet_up.user=bet.user
            
            await session.commit()
            return bet_up
        else:
            raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Aposta não encontrada..."))

@router.delete('/{bet_id}',  
            status_code=status.HTTP_204_NO_CONTENT)
async def delete_bet(bet_id: int, bet: BetSchema,
                    db: AsyncSession = Depends(get_session)):
    pass
    async with db as session:
        query = select(BetModel).filter(BetModel.id == bet_id)
        result = await session.execute(query)
        bet_del = result.scalar_one_or_none()
        if bet_del:
            await session.delete(bet_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Aposta não encontrada..."))

