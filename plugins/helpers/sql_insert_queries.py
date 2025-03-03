class SqlInsertQueries:

    songplay_table_insert = ("""
        SELECT
                md5(events.sessionid || events.start_time) songplay_id,
                events.start_time, 
                events.userid, 
                events.level, 
                songs.song_id, 
                songs.artist_id, 
                events.sessionid, 
                events.location, 
                events.useragent
        FROM 
            (SELECT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time, *
            FROM staging_events
            WHERE page='NextSong' AND userid IS NOT NULL) events
        LEFT JOIN staging_songs songs
            ON events.song = songs.title
                AND events.artist = songs.artist_name
                AND events.length = songs.duration;
    """)

    song_table_insert = ("""
        SELECT distinct song_id, title, artist_id, year, duration
        FROM staging_songs
        WHERE song_id IS NOT NULL;
    """)

    artist_table_insert = ("""
        SELECT distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude
        FROM staging_songs
        WHERE artist_id IS NOT NULL;
    """)

    user_table_insert = ("""
        SELECT distinct userid, firstname, lastname, gender, level
        FROM staging_events
        WHERE userId IS NOT NULL AND page='NextSong';
    """)

    time_table_insert = ("""
        SELECT start_time, extract(HOUR FROM start_time), extract(DAY FROM start_time), extract(WEEK FROM start_time), 
               extract(MONTH FROM start_time), extract(YEAR FROM start_time), extract(DAYOFWEEK FROM start_time)
        FROM songplays
        WHERE start_time IS NOT NULL;
    """)