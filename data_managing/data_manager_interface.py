from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def list_all_users(self):
        """Return a list of all users in the database."""
        pass

    @abstractmethod
    def list_user_movies(self, user_id):
        """
        Return a list of all movies of a specific user.

        Args:
            user_id (int): The ID of the user to fetch movies for.
        """
        pass

    @abstractmethod
    def add_user(self, user):
        """
        Add a new user to the database.

        Args:
            user (User): The User instance to add to the database.
        """
        pass

    @abstractmethod
    def add_movie(self, movie):
        """
        Add a new movie to the database.

        Args:
            movie (Movie): The Movie instance to add to the database.
        """
        pass

    @abstractmethod
    def update_movie(self, movie):
        """
        Update the details of a specific movie in the database.

        Args:
            movie (Movie): The updated Movie instance.
        """
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """
        Delete a specific movie from the database.

        Args:
            movie_id (int): The ID of the movie to delete.
        """
        pass

    @abstractmethod
    def add_review(self, review):
        pass

    @abstractmethod
    def update_review(self, review):
        pass
