def check_create(self, repo, create_dto):
    expected_return = "persisted"
    repo.persist.return_value = expected_return

    service = self.service(repo)
    result = service.create(create_dto)

    assert result == expected_return


def check_find_all_by_user(self, repo):
    expected_return = "all found"
    repo.find_by_user.return_value = expected_return

    service = self.service(repo)
    result = service.find_all_by_user(user_id=1)

    assert result == expected_return


def check_update(self, repo, update_dto):
    expected_return = "updated"
    repo.update.return_value = expected_return

    service = self.service(repo)
    result = service.update(update_dto)

    assert result == expected_return


def check_delete(self, repo):
    expected_return = "deleted"
    repo.delete.return_value = expected_return

    service = self.service(repo)
    result = service.delete(_id=1, user_id=99)

    assert result == expected_return
