all_users = User.objects.all()

for u in all_users:
        print(u.slug)
        print(u.membership_expires_at)
        u.membership_expires_at =  u.membership_expires_at + datetime.timedelta(days=2000)
        u.save()
