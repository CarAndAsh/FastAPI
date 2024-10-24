import asyncio

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.sql.functions import count

from core.models import OrderProductAssociation
from core.models import db_helper, User, Post, Profile, Order, Product


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print('user', user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)

    # result: Result = await session.execute(stmt)
    # user: User | None = result.scalar_one_or_none()

    # user: User = result.scalar_one()

    user: User | None = await session.scalar(stmt)
    print('found user', username, user)
    return user


async def create_profile(
        session: AsyncSession,
        user_id: int,
        first_name: str | None = None,
        last_name: str | None = None
) -> Profile:
    profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name)
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    for user in users:
        print(user, user.profile.first_name)


async def create_posts(session: AsyncSession, user_id: int, *posts_titles: str) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(session: AsyncSession):
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    stmt = select(User).options(selectinload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print('*' * 20)
        for post in user.posts:
            print('-', post)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)
    for post in posts:
        print(post)


async def get_users_with_posts_and_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile), selectinload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print('*' * 20)
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print('-', post)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(
            joinedload(Profile.user)
            .selectinload(User.posts)
        )
        .where(User.username == 'gru')
        .order_by(Profile.id)
    )
    profiles = await session.scalars(stmt)
    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def one_to_one_or_to_many_relations(session: AsyncSession):
    # create users
    # await create_user(session=session, username='Johanna')
    # await create_user(session=session, username='gru')

    # found users
    # user_maximus = await get_user_by_username(session=session, username='maximus')
    # user_gru = await get_user_by_username(session=session, username='gru')

    # create profiles
    # await create_profile(session=session, user_id=user_maximus.id, first_name='Maximus')
    # await create_profile(session=session, user_id=user_gru.id, first_name='Gru')

    # add posts
    # await create_posts(session, user_maximus.id, 'Intro in Python', 'New few in Python 3.13', 'Outro')
    # await create_posts(session, user_gru.id, 'Intro in FastAPI', 'New few in FastAPI')

    # await show_users_with_profiles(session=session)
    # await get_users_with_posts(session)
    # await get_posts_with_authors(session)
    # await get_users_with_posts_and_profiles(session)
    await get_profiles_with_users_and_users_with_posts(session)


async def create_order(session: AsyncSession, promocode: str | None = None) -> Order:
    order = Order(promocode=promocode)
    session.add(order)
    await session.commit()
    return order


async def create_product(
        session: AsyncSession,
        name: str,
        description: str,
        price: int
) -> Product:
    product = Product(name=name, description=description, price=price)
    session.add(product)
    await session.commit()
    return product


async def create_orders_and_products(session: AsyncSession):
    # create orders
    # order_1 = await create_order(session)
    # order_1_promo = await create_order(session, 'promo')

    # create products
    # mouse = await create_product(session, 'Mouse', '7-btn mouse', 20)
    # keyboard = await create_product(session, 'Keyboard', 'Gaming BT-keyboard', 50)
    # display = await create_product(session, 'Display', 'HQ LCD 19\" display', 490)

    # associate products with orders
    # order_1 = await session.scalar(
    #     select(Order).where(Order.id == order_1.id).options(selectinload(Order.products),))
    # order_1_promo = await session.scalar(
    #     select(Order).where(Order.id == order_1_promo.id).options(selectinload(Order.products),))
    #
    # order_1.products.append(keyboard)
    # order_1.products.append(mouse)

    # order_1_promo.products.append(keyboard)
    # order_1_promo.products.append(display)

    # order_1_promo.products = [keyboard, display]

    await session.commit()


async def get_orders_with_products(session: AsyncSession) -> list[Order]:
    stmt = select(Order).options(selectinload(Order.products)).order_by(Order.id)
    orders = await session.scalars(stmt)
    return list(orders)


async def demo_many_to_many(session: AsyncSession):
    orders = await get_orders_with_products(session)
    for order in orders:  # type: Order
        print(order.id, order.promocode, order.created_at, 'products:')
        for product in order.products:  # type: Product
            print('-', product.id, product.name, product.description, product.price)


async def get_orders_with_products_associated(session: AsyncSession) -> list[Order]:
    stmt = select(Order).options(
        selectinload(Order.products_details)
        .joinedload(OrderProductAssociation.product)
    ).order_by(Order.id)
    orders = await session.scalars(stmt)
    return list(orders)


async def demo_many_to_many_associated(session: AsyncSession):
    orders = await get_orders_with_products_associated(session)
    for order in orders:  # type: Order
        print(order.id, order.promocode, order.created_at, 'products:')
        for order_product_details in order.products_details:  # type: OrderProductAssociation
            print('-', order_product_details.product.name, order_product_details.product.price,
                  order_product_details.count)


async def create_gift_for_existing_product(session: AsyncSession):
    orders = await get_orders_with_products_associated(session)
    gift = await create_product(session, 'Gift', 'Gift for buyer', 0)
    for order in orders:
        # NOT like this - order.products_details.append(gift)
        order.products_details.append(OrderProductAssociation(count=1, unit_price=0, product=gift))
    await session.commit()


async def main():
    async with db_helper.session_factory() as session:
        # await one_to_one_or_to_many_relations(session)
        # await demo_many_to_many_associated(session)
        await create_gift_for_existing_product(session)


if __name__ == '__main__':
    asyncio.run(main())
