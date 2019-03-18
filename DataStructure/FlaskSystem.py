

class Relation:

    def __init__(self, flask, line):
        self.Line = line
        self.Flask = flask


class Flask:

    def __init__(self, value):
        self.Value = value
        self.Parents = None
        self.Siblings = None
        self.Children = None
        self.FlaskPointer = self

    def InsertRelation(self, flask_relation_container, relation):

        if relation.Line is not None:
            if relation.Line.lower() == "all":
                raise Exception("FlaskSystem could not accept", relation.Line.lower(), "as the Line. The 'all' (case insensitive) Line is used to call all available Relations (either Parents/Siblings/Children).")
        if flask_relation_container is None:
            flask_relation_container = relation
        elif isinstance(flask_relation_container, list):
            flask_relation_container.append(relation)
        else: 
            flask_relation_container = [flask_relation_container, relation]
        return flask_relation_container

    def AddParent(self, new_flask_value, line=None):

        NewFlask = Flask(new_flask_value)
        NewFlask.Children = self.InsertRelation(NewFlask.Children, Relation(self, line))
        self.Parents = self.InsertRelation(self.Parents, Relation(NewFlask, line))

    def AddSibling(self, new_flask_value, line=None):

        NewFlask = Flask(new_flask_value)
        NewFlask.Siblings = self.InsertRelation(NewFlask.Siblings, Relation(self, line))
        self.Siblings = self.InsertRelation(self.Siblings, Relation(NewFlask, line))

    def AddChild(self, new_flask_value, line=None):

        NewFlask = Flask(new_flask_value)
        NewFlask.Parents = self.InsertRelation(NewFlask.Parents, Relation(self, line))
        self.Children = self.InsertRelation(self.Children, Relation(NewFlask, line))

    def ConnectParent(self, flask, line=None):

        flask.Children = self.InsertRelation(flask.Children, Relation(self, line))
        self.Parents = self.InsertRelation(self.Parents, Relation(flask, line))

    def ConnectSibling(self, flask, line=None):

        flask.Siblings = self.InsertRelation(flask.Siblings, Relation(self, line))
        self.Siblings = self.InsertRelation(self.Siblings, Relation(flask, line))

    def ConnectChild(self, flask, line=None):

        flask.Parents = self.InsertRelation(flask.Parents, Relation(self, line))
        self.Children = self.InsertRelation(self.Children, Relation(flask, line))

    def ConvertRelationsToFlasks(self, flask_relation_container):

        retrieved_flasks = None
        if isinstance(flask_relation_container, list):
            for flask_relation in flask_relation_container:
                if retrieved_flasks is None:
                    retrieved_flasks = flask_relation.Flask
                elif isinstance(retrieved_flasks, list):
                    retrieved_flasks.append(flask_relation.Flask)
                else:
                    retrieved_flasks = [retrieved_flasks]
                    retrieved_flasks.append(flask_relation.Flask)
        else:
            retrieved_flasks = flask_relation_container.Flask
        return retrieved_flasks

    def RetrieveFlasksFiltered(self, flask_relation_container, line):

        if isinstance(flask_relation_container, list):
            for flask_relation in flask_relation_container:
                if flask_relation.Line != line:
                    flask_relation_container.remove(flask_relation)
        retrieved_flasks = self.ConvertRelationsToFlasks(flask_relation_container)
        return retrieved_flasks

    def RetrieveFlasks(self, flask_relation_container, line):

        if flask_relation_container is not None:
            if line is not None:
                if line.lower() != "all":
                    retrieved_flasks = self.RetrieveFlasksFiltered(flask_relation_container, line)
                elif line.lower() == "all":
                    retrieved_flasks = self.ConvertRelationsToFlasks(flask_relation_container)
            else:
                retrieved_flasks = self.RetrieveFlasksFiltered(flask_relation_container, line)

        return retrieved_flasks

    def GetParent(self, line=None):

        retrieved_flasks = self.RetrieveFlasks(self.Parents, line)
        return retrieved_flasks

    def GetSibling(self, line=None):

        retrieved_flasks = self.RetrieveFlasks(self.Siblings, line)
        return retrieved_flasks

    def GetChild(self, line=None):

        retrieved_flasks = self.RetrieveFlasks(self.Children, line)
        return retrieved_flasks

    def UpdateValue(self, value):

        self.Value = value

    def GetPointer(self):

        return self.FlaskPointer

    def MovePointerToParent(self, line=None):

        self.FlaskPointer = self.FlaskPointer.GetParent(line)

    def MovePointerToSibling(self, line=None):

        self.FlaskPointer = self.FlaskPointer.GetSibling(line)

    def MovePointerToChild(self, line=None):

        self.FlaskPointer = self.FlaskPointer.GetChild(line)

    def MovePointerToFlask(self, flask):

        self.FlaskPointer = flask

    def ResetPointer(self):

        self.FlaskPointer = self

    def ShowRelatedFlasks(self, flask_relation_container):

        if isinstance(flask_relation_container, list):
            for flask_relation in flask_relation_container:
                print("\t", flask_relation.Flask.Value, flask_relation.Line)
        elif flask_relation_container:
            print("\t", flask_relation_container.Flask.Value, flask_relation_container.Line)
        else:
            print("\t", flask_relation_container)

    def ShowFlaskProperties(self):

        print("RELATED PARENTS:")
        self.ShowRelatedFlasks(self.Parents)
        print("CURRENT FLASK:")
        print("\t", self.Value)
        print("RELATED SIBLINGS:")
        self.ShowRelatedFlasks(self.Siblings)
        print("RELATED CHILDREN:")
        self.ShowRelatedFlasks(self.Children)
        print("")

    def GenerateAncestralLines(self):

        self.ResetPointer()
        AncestralLines = []
        Reserved = None
        Reserve = None
        SavedList = [self.GetPointer().Value]
        while Reserved != []:
            if self.GetPointer().Parents is None:
                AncestralLines.append(SavedList)
            else:
                if isinstance(self.GetPointer().Parents, list):
                    for flask_parent in self.GetPointer().Parents:
                        if Reserved is None:
                            Reserved = [[flask_parent.Flask, SavedList]]
                        else:
                            Reserved.append([flask_parent.Flask, SavedList])
                else:
                    if Reserved is None:
                        Reserved = [[self.GetPointer().Parents.Flask, SavedList]]
                    else:
                        Reserved.append([self.GetPointer().Parents.Flask, SavedList])
            if Reserve in Reserved:
                Reserved.remove(Reserve)
            if len(Reserved) != 0:
                Reserve = Reserved[0]
                self.MovePointerToFlask(Reserve[0])
                SavedList = Reserve[1] + [self.GetPointer().Value]
        self.ResetPointer()
        return AncestralLines

    def GenerateDescendantLines(self):

        self.ResetPointer()
        DescendantLines = []
        Reserved = None
        Reserve = None
        SavedList = [self.GetPointer().Value]
        while Reserved != []:
            if self.GetPointer().Children is None:
                DescendantLines.append(SavedList)
            else:
                if isinstance(self.GetPointer().Children, list):
                    for flask_child in self.GetPointer().Children:
                        if Reserved is None:
                            Reserved = [[flask_child.Flask, SavedList]]
                        else:
                            Reserved.append([flask_child.Flask, SavedList])
                else:
                    if Reserved is None:
                        Reserved = [[self.GetPointer().Children.Flask, SavedList]]
                    else:
                        Reserved.append([self.GetPointer().Children.Flask, SavedList])
            if Reserve in Reserved:
                Reserved.remove(Reserve)
            if len(Reserved) != 0:
                Reserve = Reserved[0]
                self.MovePointerToFlask(Reserve[0])
                SavedList = Reserve[1] + [self.GetPointer().Value]
        self.ResetPointer()
        return DescendantLines

    def GenerateFlippedAncestralLines(self):

        AncestralLines = self.GenerateAncestralLines()
        AncestralLines = [AncestralLine[::-1] for AncestralLine in AncestralLines]
        return AncestralLines

    def GenerateFlippedDescendantLines(self):

        DescendantLines = self.GenerateDescendantLines()
        DescendantLines = [DescendantLine[::-1] for DescendantLine in DescendantLines]
        return DescendantLines
