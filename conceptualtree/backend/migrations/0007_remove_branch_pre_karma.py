# Generated by Django 4.1.7 on 2023-02-28 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_branch_pre_karma'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branch',
            name='pre_karma',
        ),
        migrations.RunSQL(
            # SQL-код создания процедуры
            '''
            CREATE OR REPLACE PROCEDURE update_karma() as $$
            BEGIN
            
            
            update backend_relations
            set parent_karma = NULL;
            
            
            update backend_relations
            set parent_karma = backend_branch.likes
            from backend_relations as br
            Right join backend_branch on br.child_id = backend_branch.id
            where br.child_id is Null and backend_relations.parent_id = backend_branch.id;
            
            -- in loop while exist parent_karma is null
            WHILE EXISTS (SELECT 1 FROM backend_relations WHERE parent_karma IS NULL) LOOP
            update backend_relations
            set parent_karma = se.karma + backend_branch.likes
            from
                (select br.parent_id as parent, sum(br_parent.parent_karma) as karma
                from backend_relations as br
                join backend_relations as br_parent
                on br.parent_id = br_parent.child_id
                join backend_branch on br.parent_id = backend_branch.id
                LEFT JOIN backend_relations AS br_null
                ON br.parent_id = br_null.child_id AND br_null.parent_karma IS NULL
                where br.parent_karma is NULL
                AND br_null.child_id IS NULL
                group by br.parent_id
                ) se
            join backend_branch on se.parent = backend_branch.id
            where parent_id = se.parent;
            -- end loop
            END LOOP;
            
            update backend_branch
            set karma = 0;
            
            update backend_branch
            set karma = sel.karma
            from
            (select br.parent_id as idiot, round(avg(brc.parent_karma)/2) as karma
            from backend_relations as br
            join backend_relations as brc on br.child_id = brc.child_id
            group by br.parent_id) as sel
            where backend_branch.id = sel.idiot;
            
            update backend_branch
            set karma = backend_branch.karma + sel.karma
            from
            (select br.child_id as idiot, sum(br.parent_karma) as karma
            from backend_relations as br
            group by br.child_id) as sel
            where backend_branch.id = sel.idiot;
            
            END;
            $$ LANGUAGE plpgsql;
            
            
            CREATE OR REPLACE FUNCTION check_cyclicity() RETURNS trigger AS $$
            DECLARE
              found_cycle boolean;
            BEGIN
                IF (select count(*) from backend_relations where backend_relations.child_id = NEW.parent_id) = 0  THEN
                RETURN NEW;
              END IF;
              -- Check for cyclicity in the updated rows
              WITH RECURSIVE search_graph(child_id, parent_id, depth, path) AS (
                SELECT child_id, parent_id, 1, ARRAY[child_id]
                FROM backend_relations
                UNION ALL
                SELECT ur.child_id, ur.parent_id, sg.depth + 1, path || ur.child_id
                FROM search_graph sg, backend_relations ur
                WHERE sg.parent_id = ur.child_id AND NOT ur.child_id = ANY(path)
              )
              SELECT 1 FROM search_graph WHERE child_id = NEW.parent_id LIMIT 1 INTO found_cycle;
            
              IF found_cycle THEN
                RAISE EXCEPTION 'Cyclicity detected';
              END IF;
            
              RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            
            
            
            CREATE or replace TRIGGER check_cyclicity_trigger
            BEFORE INSERT or update ON backend_relations
            FOR EACH ROW
            EXECUTE FUNCTION check_cyclicity();
            ''',
            reverse_sql=migrations.RunSQL.noop
        ),
    ]
