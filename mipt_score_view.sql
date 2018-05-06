DROP VIEW mipt_ratings;
CREATE VIEW mipt_ratings AS
SELECT
    (like_count + 1) / (mean_likes + 1) AS likes, (comment_count + 1) / (mean_comments + 1) AS comments,
    mipt_follower_count * 1. / follower_count AS mipt_followers_part,
    author_username, caption, mipt_follower_count, link
FROM
    instagram_medias
    JOIN (
        SELECT
            *
        FROM
            instagram_users
        INNER JOIN (
                SELECT
                    followee_id,
                    count(*) AS mipt_follower_count
                FROM
                    instagram_followships
                WHERE
                    followee_id IN (
                        SELECT
                            user_id
                        FROM
                            instagram_mipt_users)
                    GROUP BY
                        followee_id) mipt_followers_count
                        ON mipt_followers_count.followee_id = instagram_users.user_id) mipt_users
                ON mipt_users.user_id = instagram_medias.author_id
where
	link is not NULL AND likes is not NULL and
	taken_at >= date('now', '-7 day')
