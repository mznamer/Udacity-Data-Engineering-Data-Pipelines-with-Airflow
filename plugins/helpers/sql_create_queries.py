class SqlCreateQueries:

    staging_events_table_create = """
        CREATE TABLE IF NOT EXISTS public.staging_events (
            artist varchar(256),
            auth varchar(256),
            firstname varchar(256),
            gender varchar(256),
            iteminsession int4,
            lastname varchar(256),
            length numeric(18,0),
            "level" varchar(256),
            location varchar(256),
            "method" varchar(256),
            page varchar(256),
            registration numeric(18,0),
            sessionid int4,
            song varchar(256),
            status int4,
            ts int8,
            useragent varchar(256),
            userid int4
        );
    """

    staging_songs_table_create = """
        CREATE TABLE IF NOT EXISTS public.staging_songs (
            num_songs int4,
            artist_id varchar(256),
            artist_name varchar(256),
            artist_latitude numeric(18,0),
            artist_longitude numeric(18,0),
            artist_location varchar(256),
            song_id varchar(256),
            title varchar(256),
            duration numeric(18,0),
            "year" int4
        );
    """

    songplays_table_create = """
        CREATE TABLE IF NOT EXISTS public.songplays (
            playid varchar(32) PRIMARY KEY,
            start_time timestamp NOT NULL,
            userid int4 NOT NULL,
            "level" varchar(256),
            songid varchar(256),
            artistid varchar(256),
            sessionid int4,
            location varchar(256),
            user_agent varchar(256)
        );
    """

    songs_table_create = """
        CREATE TABLE IF NOT EXISTS public.songs (
            songid varchar(256) PRIMARY KEY,
            title varchar(256),
            artistid varchar(256),
            "year" int4,
            duration numeric(18,0)
        );
    """

    artists_table_create = """
        CREATE TABLE IF NOT EXISTS public.artists (
            artistid varchar(256) PRIMARY KEY,
            name varchar(256),
            location varchar(256),
            lattitude numeric(18,0),
            longitude numeric(18,0)
        );
    """

    users_table_create = """
        CREATE TABLE IF NOT EXISTS public.users (
            userid int4 PRIMARY KEY,
            first_name varchar(256),
            last_name varchar(256),
            gender varchar(256),
            "level" varchar(256)
        );
    """

    time_table_create = """
        CREATE TABLE IF NOT EXISTS public."time" (
            start_time timestamp PRIMARY KEY,
            "hour" int4,
            "day" int4,
            week int4,
            "month" varchar(256),
            "year" int4,
            weekday varchar(256)
        );
    """