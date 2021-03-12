from datetime import datetime, timedelta

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from auth.helpers import set_session_cookie
from auth.models import Session
from users.models.user import User
from users.models.invites import Invite


def apply_invite(request):
    if request.me:
        return redirect("index")

    code = request.GET.get('code')
    if not code:
        return redirect("index", permanent=False)

    try:
        invite = Invite.objects.get(id=code)
    except Invite.DoesNotExist:
        return render(request, "error.html", {
            "title": "Неверный инвайт код 🤔",
            "message": "Инвайт с таком кодом не найден. "
                        "Попробуйте ввести код еще раз. "
        })
    if invite.used_by:
        return render(request, "error.html", {
            "title": "Инвайт код уже использован 😛",
            "message": "Кто-то уже использовал этот инвайт.",
        })

    email = request.GET.get('email')
    if not email:
        return render(request, "auth/invite.html")

    email = email.lower()
    now = datetime.utcnow()
    user, is_created = User.objects.get_or_create(
        email=email,
        defaults=dict(
            membership_platform_type=User.MEMBERSHIP_PLATFORM_DIRECT,
            full_name=email[:email.find("@")],
            membership_started_at=now,
            membership_expires_at=now + timedelta(days=invite.membership_days),
            created_at=now,
            updated_at=now,
            moderation_status=User.MODERATION_STATUS_INTRO,
        ),
    )

    if not is_created:
        return render(request, "error.html", {
            "title": "Этот email уже зарегистрирован 😛",
            "message": "В клубе уже есть пользователь с указанным вами email.",
        })

    invite.used_by = user
    invite.save()

    # if is_created:
    #     Post.upsert_user_intro(user, "Интро как интро, аппрув прошло :Р", is_visible=True)

    session = Session.create_for_user(user)
    return set_session_cookie(redirect("profile", user.slug), user, session)


def user_invites(request, user_slug):
    if user_slug == "me":
        return redirect("user_invites", request.me.slug, permanent=False)

    user = get_object_or_404(User, slug=user_slug)
    if user.id != request.me.id and not request.me.is_god:
        raise Http404()

    invites = user.invites.all()
    active_invites = [i for i in invites if not i.used_by]
    used_invites = [i for i in invites if i.used_by]

    return render(request, "users/invites.html", {
        "user": user,
        "active_invites": active_invites,
        "used_invites": used_invites,
    })
